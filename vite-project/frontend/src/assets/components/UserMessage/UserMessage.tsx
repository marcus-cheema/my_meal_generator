// import '../../App.css';
import styles from './UserMessage.module.css'
import 'bootstrap/dist/css/bootstrap-grid.min.css'

interface UserMessageProps {
    submittedMessage: string;
}

function UserMessage(props: UserMessageProps) {
    return (
        <div className={`${styles.userMessage} card`}>
            <div className="card-body"> {props.submittedMessage} </div>
        </div>
    )
}

export default UserMessage