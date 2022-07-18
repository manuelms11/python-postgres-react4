import {useEffect,useState} from 'react' //hooks
import axios from 'axios'
import {format} from 'date-fns'
import './App.css';


const baseURL = 'http://localhost:5000/'

function App() {
  const [description, setDescription] = useState("");
  const [eventsList, setEventsList] = useState([]);
  

  const fetchEvents =  async () => {
    const data = await axios.get(`${baseURL}/events`)  
    const { events } = data.data
    setEventsList(events);
    console.log("DATA: ",data)
  }

  const handleChange = e => {
    setDescription(e.target.value);
  }

  const handleSubmit = async (e) =>{  
    e.preventDefault();
    try{
      const data = await axios.post(`${baseURL}/events`, {description}) 
      setEventsList([...eventsList,data.data]);
      setDescription('')
    } catch(err){
      console.error(err.message)
    }   
    console.log(description);
  }

  useEffect(() => {
    fetchEvents();
  }, [])

  return (
    <div className="App-header">
      <section >
        <form onSubmit={handleSubmit}>
          <label htmlFor="description">Description</label>  
          <input onChange={handleChange} type="text" name="description" id="description" value={description}/>
        </form>
        <button type="submit">Submit</button>  
      </section>
      <section>
        <ul>
          {eventsList.map(event =>{
            return( <li key={event.id}>{event.description}</li> )
          })}
        </ul>
      </section>  
      
    </div>
  );
}

export default App;
