// import '../../App.css';
import styles from './ChatBotBox.module.css'
import 'bootstrap/dist/css/bootstrap-grid.min.css'
import { useState, KeyboardEvent } from 'react'
import TextInput from '../TextInput/TextInput';
import InputButton from '../InputButton/InputButton';
import UserMessage from '../UserMessage/UserMessage';
import BotResponse from '../BotResponse/BotResponse';
import UserInfoForm from '../UserInfoForm/UserInfoForm';
import { sendMessage, getBotResponse } from '../../../services/apiServices'

function ChatBotBox() {
    let [userMessage, setUserMessage] = useState('') // manage the state of what is in the TextInput. For every change, update userMessage
    
    let [submittedMessages, setSubmittedMessages] = useState<string[]>([]); // store all submitted messages
    let [botResponses, setBotResponses]           = useState<string[]>([]); // store all bot responses

    let [userMessageCount, setUserMessageCount] = useState(0) // keep track of # of valid messages for stable UI
    let [botResponseCount, setBotResponseCount] = useState(0)

    let handleClick = async() => { // don't need to specify MouseEvent here, b/c already specified in UserTextButton
        setUserMessage('');
        if (userMessage !== '') {
            setUserMessage('');
            setSubmittedMessages([...submittedMessages, userMessage]); // update the message display textbox
            setUserMessageCount(userMessageCount + 1); 
            try {
                await sendMessage(userMessage);

                let botResponse = await getBotResponse();
                setBotResponses([...botResponses, botResponse]);
                setBotResponseCount(botResponseCount + 1);
            } catch(error) {
                console.error("Error sending message", error);
            }
        }
    }

    let handleEnter = (e: KeyboardEvent) => {
        if (e.key === 'Enter') { 
            e.preventDefault();
            handleClick(); 
        }
    }

    return(
        <div className={styles.chatBotBox}>
            <div className={styles.userFormContainer}>
                <UserInfoForm/>
            </div>

            <div className={styles.userMessageContainer}>
                {submittedMessages.map((message, index) => (
                    <div key={index}>
                        <UserMessage submittedMessage={message} />
                        {botResponses[index] && (
                            <BotResponse responseMessage={botResponses[index]} />
                        )}
                    </div>
                ))}
            </div>

            <div className={styles.inputMessage}>
                <TextInput userMessage={userMessage} setUserMessage={setUserMessage} onKeyDown={handleEnter}/>
                <InputButton handleClick={ handleClick } />
            </div>

        </div>
    )
}
export default ChatBotBox;