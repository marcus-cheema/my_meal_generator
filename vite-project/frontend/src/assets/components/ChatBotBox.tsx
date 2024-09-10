import '../../App.css';
import 'bootstrap/dist/css/bootstrap-grid.min.css'
import { useState, KeyboardEvent } from 'react'
import TextInput from './TextInput';
import UserTextButton from './UserTextButton';
import UserMessage from './UserMessage';
import BotResponse from './BotResponse';
import { sendMessage, getBotResponse } from '../../services/apiServices'

function ChatBotBox() {
    let [userMessage, setUserMessage] = useState('') // manage the state of what is in the TextInput. For every change, update userMessage
    
    let [submittedMessages, setSubmittedMessages] = useState<string[]>([]); // store all submitted messages
    let [botResponses, setBotResponses]           = useState<string[]>([]); // store all bot responses

    let [userMessageCount, setUserMessageCount] = useState(0) // keep track of # of valid messages for stable UI
    let [botResponseCount, setBotResponseCount] = useState(0)
    
    let valid_send_flag = false

    async function handleClick() { // don't need to specify MouseEvent here, b/c already specified in UserTextButton
        if (userMessage !== '') { 
            setSubmittedMessages([...submittedMessages, userMessage]); // update the message display textbox
            setUserMessageCount(userMessageCount + 1); 
           
            await sendMessage(userMessage).then(function(response) {
                console.log("Response: ", response.status);
                if (response.status === 200) { 
                    valid_send_flag = true;
                } else {
                    console.log("this didn't work");
                    valid_send_flag = false;
                }
            }).catch(function(error) {
                console.log(error);
            })

            if (valid_send_flag) {
                await getBotResponse().then(function(response) {
                    setBotResponses([...botResponses, response]);
                    setBotResponseCount(botResponseCount + 1);
                }).catch(function(error) {
                    console.log(error);
                })
            }
        }
        setUserMessage(''); // delete typed message after submission
        console.log("We have " + botResponseCount + " messages");
    }

    let handleEnter = (e: KeyboardEvent) => {
        if (e.key === 'Enter') { handleClick(); }
    }

    return(
        <div className="chat-bot-box">
            
            <div className="user-message-container">
                {submittedMessages.map((message, index) => (
                    <div key={index}>
                        <UserMessage submittedMessage={message} />
                        {botResponses[index] && (
                            <BotResponse responseMessage={botResponses[index]} />
                        )}
                    </div>
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