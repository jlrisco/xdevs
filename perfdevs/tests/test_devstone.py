from unittest import TestCase, TestLoader, TestSuite, TextTestRunner

from perfdevs.sim import Coordinator
from perfdevs.examples.devstone.devstone import LI, HI
from perfdevs.models import Atomic, Coupled

import random


class Utils:

    @staticmethod
    def count_atomics(coupled):
        """
        :return: Number of atomic components in a coupled model
        """
        atomic_count = 0
        for comp in coupled.components:
            if isinstance(comp, Atomic):
                atomic_count += 1
            elif isinstance(comp, Coupled):
                atomic_count += Utils.count_atomics(comp)
            else:
                raise RuntimeError("Unrecognized type of component")

        return atomic_count

    @staticmethod
    def count_ic(coupled):
        """
        :return: Number of ic couplings in a coupled model
        """
        ic_count = len(coupled.ic)
        for comp in coupled.components:
            if isinstance(comp, Coupled):
                ic_count += Utils.count_ic(comp)
            elif not isinstance(comp, Atomic):
                raise RuntimeError("Unrecognized type of component")

        return ic_count

    @staticmethod
    def count_eic(coupled):
        """
        :return: Number of eic couplings in a coupled model
        """
        eic_count = len(coupled.eic)
        for comp in coupled.components:
            if isinstance(comp, Coupled):
                eic_count += Utils.count_eic(comp)
            elif not isinstance(comp, Atomic):
                raise RuntimeError("Unrecognized type of component")

        return eic_count

    @staticmethod
    def count_eoc(coupled):
        """
        :return: Number of eoc couplings in a coupled model
        """
        eoc_count = len(coupled.eoc)
        for comp in coupled.components:
            if isinstance(comp, Coupled):
                eoc_count += Utils.count_eoc(comp)
            elif not isinstance(comp, Atomic):
                raise RuntimeError("Unrecognized type of component")

        return eoc_count

    @staticmethod
    def count_transitions(coupled):
        """
        :return: Number of atomic components in a coupled model
        """
        int_count = 0
        ext_count = 0
        for comp in coupled.components:
            if isinstance(comp, Atomic):
                int_count += comp.int_count
                ext_count += comp.ext_count
            elif isinstance(comp, Coupled):
                pic, pec = Utils.count_transitions(comp)
                int_count += pic
                ext_count += pec
            else:
                raise RuntimeError("Unrecognized type of component")

        return int_count, ext_count


class DevstoneUtilsTestCase(TestCase):

    def __init__(self, name, num_valid_params_sets: int = 10):
        super().__init__(name)
        self.valid_high_params = []
        self.valid_low_params = []

        for _ in range(int(num_valid_params_sets)):
            self.valid_high_params.append([random.randint(1, 100), random.randint(1, 200),
                                           random.randint(1, 1000), random.randint(1, 1000)])

        for _ in range(int(num_valid_params_sets)):
            self.valid_low_params.append([random.randint(1, 20), random.randint(1, 30),
                                      random.randint(1, 1000), random.randint(1, 1000)])


class TestLI(DevstoneUtilsTestCase):

    def test_structure(self):
        """
        Check structure params: atomic modules, ic's, eic's and eoc's.
        """
        for params_tuple in self.valid_high_params:
            params = dict(zip(("depth", "width", "int_delay", "ext_delay"), params_tuple))

            with self.subTest(**params):
                li_root = LI("LI_root", **params)
                self.assertEqual(Utils.count_atomics(li_root), (params["width"] - 1) * (params["depth"] - 1) + 1)
                self.assertEqual(Utils.count_eic(li_root), params["width"] * (params["depth"] - 1) + 1)
                self.assertEqual(Utils.count_eoc(li_root), params["depth"])
                self.assertEqual(Utils.count_ic(li_root), 0)

    def test_behavior(self):
        """
        Check behaviour params: number of int and ext transitions.
        """
        for params_tuple in self.valid_low_params:
            params = dict(zip(("depth", "width", "int_delay", "ext_delay"), params_tuple))

            with self.subTest(**params):
                li_root = LI("LI_root", **params)
                coord = Coordinator(li_root, flatten=False, force_chain=False)
                coord.initialize()
                coord.inject(li_root.i_in, 0)
                coord.simulate()

                int_count, ext_count = Utils.count_transitions(li_root)
                self.assertEqual(int_count, (params["width"] - 1) * (params["depth"] - 1) + 1)
                self.assertEqual(ext_count, (params["width"] - 1) * (params["depth"] - 1) + 1)

class TestHI(DevstoneUtilsTestCase):

    def test_structure(self):
        """
        Check structure params: atomic modules, ic's, eic's and eoc's.
        """
        for params_tuple in self.valid_high_params:
            params = dict(zip(("depth", "width", "int_delay", "ext_delay"), params_tuple))

            with self.subTest(**params):
                hi_root = HI("HI_root", **params)
                self.assertEqual(Utils.count_atomics(hi_root), (params["width"] - 1) * (params["depth"] - 1) + 1)
                self.assertEqual(Utils.count_eic(hi_root), params["width"] * (params["depth"] - 1) + 1)
                self.assertEqual(Utils.count_eoc(hi_root), params["depth"])
                self.assertEqual(Utils.count_ic(hi_root), (params["width"] - 2) * (params["depth"] - 1) if params["width"] > 2 else 0)

    def test_behavior(self):
        """
        Check behaviour params: number of int and ext transitions.
        """
        for params_tuple in self.valid_low_params:
            params = dict(zip(("depth", "width", "int_delay", "ext_delay"), params_tuple))

            with self.subTest(**params):
                hi_root = HI("HI_root", **params)
                coord = Coordinator(hi_root, flatten=False, force_chain=False)
                coord.initialize()
                coord.inject(hi_root.i_in, 0)
                coord.simulate()

                int_count, ext_count = Utils.count_transitions(hi_root)
                self.assertEqual(int_count, (((params["width"] - 1) * params["width"]) / 2) * (params["depth"] - 1) + 1)
                self.assertEqual(ext_count, (((params["width"] - 1) * params["width"]) / 2) * (params["depth"] - 1) + 1)