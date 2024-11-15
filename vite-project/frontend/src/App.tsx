import ChatBotBox from './assets/components/ChatBotBox/ChatBotBox'
// import UserInfoForm from './assets/components/UserInfoForm'
import logo from './assets/images/Mindful.png'
import 'bootstrap/dist/css/bootstrap-grid.min.css'
import './App.css'

function App() {
  return ( // see ChatBotBox.tsx
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
