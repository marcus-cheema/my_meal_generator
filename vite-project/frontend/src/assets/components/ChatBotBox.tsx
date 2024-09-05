import '../../App.css';
import 'bootstrap/dist/css/bootstrap-grid.min.css'
import { useState, KeyboardEvent } from 'react'
import TextInput from './TextInput';
import UserTextButton from './UserTextButton';
import UserMessage from './UserMessage';

function ChatBotBox() {
    let [userMessage, setUserMessage] = useState('') // manage the state of what is in the TextInput. For every change, update userMessage
    let [submittedMessages, setSubmittedMessages] = useState<string[]>([]); // store all submitted messages
    let [userMessageCount, setUserMessageCount] = useState(0)

    let handleClick = () => { // don't need to specify MouseEvent here, b/c already specified in UserTextButton
        if (userMessage !== '') { 
            setSubmittedMessages([...submittedMessages, userMessage]); // update the message display textbox
            setUserMessageCount(userMessageCount + 1); 
        }
        setUserMessage('') // delete typed message after submission
        console.log("deez nuts")
    }

    let handleEnter = (e: KeyboardEvent) => {
        if (e.key === 'Enter') { handleClick(); }
    }

    return(
        <div className="chat-bot-box">
            
            <div className="user-message-container">
                {submittedMessages.map((message, index) => (
                    <UserMessage key={index} submittedMessage={message} />
                ))}
            </div>
            
            <div className="user-text-button-container">
                <TextInput userMessage={userMessage} setUserMessage={setUserMessage} onKeyDown={handleEnter}/>
                <UserTextButton handleClick={ handleClick } />
            </div>

        </div>
    )
}

export default ChatBotBox