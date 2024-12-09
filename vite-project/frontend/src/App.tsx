import ChatBotBox from './assets/components/ChatBotBox/ChatBotBox'
import logo from './assets/images/Mindful2.png'
import 'bootstrap/dist/css/bootstrap-grid.min.css'
import './App.css'

function App() {
  return (
    <>
      <header className="app-header">
        <img src={logo} alt="Logo" className="app-logo"/>
      </header>
      <div>
        <ChatBotBox/>
      </div>
    </>
  )
}

export default App
