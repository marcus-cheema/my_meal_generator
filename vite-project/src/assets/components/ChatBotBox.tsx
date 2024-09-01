import '../../App.css';
import 'bootstrap/dist/css/bootstrap-grid.min.css'
import TextInput from './TextInput';
import UserTextButton from './UserTextButton';
import UserMessage from './UserMessage';

// interface ChatBotBoxProps {
//     height: string;
//     width: string;
// }

function ChatBotBox() {
    return(
        <div className="chat-bot-box">
            <UserMessage/>
            <div className="user-text-button-container">
                <TextInput/>
                <UserTextButton/>
            </div>
        </div>
    )
}

export default ChatBotBox