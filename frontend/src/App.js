import {useEffect,useState} from 'react' //hooks
import axios from 'axios'
import {format} from 'date-fns'
import './App.css';


const baseURL = 'http://localhost:5000/'

function App() {
  //const [description, setDescription] = useState("");
  //const [eventsList, setEventsList] = useState([]);
  const [allValues, setAllValues] = useState({
    teamName : '',
    roleName : ''
  });

  const [employeesList, setEmployeesList] = useState([]);


  //const [roleName, setRoleName] = useState("");

  const fetchEvents =  async () => {
    const data = await axios.get(`${baseURL}/employees`)  
    const { employees } = data.data
    setEmployeesList(employees);
    console.log("DATA: ",data)
  }

  /*const handleChange = e => {
    setAllValues( preValues =>{
      return {...preValues, [e.target.name]: e.target.value}
    });
  }*/

  const handleChange = e => {
    setAllValues({
      ...allValues,
      [e.target.name]: e.target.value
    });
  };

  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Methods': 'PUT, POST, GET, DELETE, PATCH, OPTIONS',
    'Access-Control-Allow-Origin': '*'
  }

  const handleSubmit = async (e) => {  
    e.preventDefault();
    console.log("Hola3")
    try{
      const data = await axios.post(`${baseURL}/employees`, {
        teamName: allValues.teamName,
        roleName: allValues.roleName
        },{
          headers: headers
        }) 
      console.log("DATA: ",data)
      //setEmployeesList([...employeesList,data.data]);
      //setAllValues('')
    } catch(err){
      console.error(err.message)
    }   
  }

  const fetchEvents2=  async (e) => {
    e.preventDefault();
    console.log('Hola');
  }

  useEffect(() => {
    fetchEvents();
  }, [])

  return (
    <div className="App-header">
      <section >
        <form onSubmit={handleSubmit}>
          <label htmlFor="teamName">Team Name</label>  
          <input onChange={handleChange} type="text" name="teamName" id="teamName" value={allValues.teamName}/>
          <label htmlFor="roleName">Role Name</label>  
          <input onChange={handleChange} type="text" name="roleName" id="roleName" value={allValues.roleName}/>
          <input type="submit" value="Submit" /> 
        </form>
        
      </section>     
      <section>
        <ul>
          {employeesList.map(employee =>{
            return( <li key={employee.id}>{employee.role_name}</li> )
          })}
        </ul>
      </section>   
    </div>
  );
}

export default App;
