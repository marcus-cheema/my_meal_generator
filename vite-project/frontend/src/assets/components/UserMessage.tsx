import '../../App.css';
import 'bootstrap/dist/css/bootstrap-grid.min.css'

interface UserMessageProps {
    submittedMessage: string;
}

function UserMessage(props: UserMessageProps) {
    return (
        <div className="card user-message">
            <div className="card-body"> {props.submittedMessage} </div>
        </div>
    )
}

export default UserMessage