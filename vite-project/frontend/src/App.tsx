import ChatBotBox from './assets/components/ChatBotBox'
import 'bootstrap/dist/css/bootstrap-grid.min.css'
import './App.css'
import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {

  let [message, setMessage] = useState('')

  let fetchAPI = async () => {
    try {
      let response = await axios.get("http://127.0.0.1:8080/api/users"); // backend URL
      console.log(response.data)
      setMessage(JSON.stringify(response.data));
    
    } catch(error) {
      console.error('Error fetching data:', error)
    }
  }

  useEffect(() => {
    fetchAPI();
  }, []);

  return ( // see ChatBotBox.tsx
    <div>
      <p>{message}</p>
      <ChatBotBox/>
    </div>  
  )
  
}

export default App
