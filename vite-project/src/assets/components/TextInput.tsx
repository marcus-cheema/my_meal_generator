import 'bootstrap/dist/css/bootstrap.min.css'
import '../../App.css'

function TextInput() {
    return (
        <form>
            <div className="text-input-parent">
                <input className="form-control form-control-lg text-input" type="text"placeholder="Ask a question"/>
            </div>
        </form>
    )
}

export default TextInput