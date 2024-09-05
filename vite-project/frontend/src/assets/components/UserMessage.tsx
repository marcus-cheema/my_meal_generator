import '../../App.css';
import 'bootstrap/dist/css/bootstrap-grid.min.css'

interface userMessageProps {
    submittedMessage: string;
}


function UserMessage(props: userMessageProps) {
    return (
        <div className="card user-message">
            <div className="card-body"> {props.submittedMessage} </div>
        </div>
    )
}

export default UserMessage