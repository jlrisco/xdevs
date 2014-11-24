package mitris.sim.core.modeling.api;

/**
 * 
 * Class that implements the basic entity needed to manage all the DEVS elements.
 * An entity is a component, atomic model, coupled model, connection, port ... everything.
 * @author José Luis Risco Martín
 * @author Saurabh Mittal
 *
 */
public interface Entity {
	/**
	 * Member funcion to get the name of the entity
	 * @return The name of this entity.
	 */
	public String getName();
	/**
	 * For debugging purposes, <code>toString</code> gives to the user useful information about the current
	 * state of this entity.
	 * @return Information about the current state of this entity
	 */
	public String toString();
	
	// TODO: Add this implementation
	/**
	 * Saurabh's comments:
	 * this is needed for netcentric Message Enterprise bus implementation.
	 * This is also de-facto way Eclipse finds various components
	 * in its plugin architecture. Allows full traceability
	 */
	// public String getQualifiedName(); 
}