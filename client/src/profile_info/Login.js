import { useState } from 'react';
import axios from "axios";

function Login(props) {

    const [loginForm, setloginForm] = useState({
        username: "",
        password: ""
    })


    // React equivalent of os.environ.get() for environment variables

    function logMeIn(event) {
        const backend_route = process.env.REACT_APP_API_URL;
        console.log(`${backend_route}/login`)

        axios.post(`${backend_route}/login`, {
            username: loginForm.username,
            password: loginForm.password
        })
            .then((response) => {
                props.setToken(response.data.access_token)
                // We generate a token in backend if log-in successfully, and we then locally store JWT
            }).catch((error) => {
                if (error.response) {
                    console.log(error.response)
                    console.log(error.response.status)
                    console.log(error.response.headers)
                }
            })

        setloginForm(({
            username: "",
            password: ""
        }))

        event.preventDefault()
    }

    function handleChange(event) {
        const { value, name } = event.target
        setloginForm(prevNote => ({
            ...prevNote, [name]: value
        })
        )
    }

    return (
        <div>
            <h1>Login</h1>
            <form className="login">
                <input onChange={handleChange}
                    type="username"
                    text={loginForm.username}
                    name="username"
                    placeholder="Username"
                    value={loginForm.username} />
                <input onChange={handleChange}
                    type="password"
                    text={loginForm.password}
                    name="password"
                    placeholder="Password"
                    value={loginForm.password} />

                <button onClick={logMeIn}>Submit</button>
            </form>
        </div>
    );
}

export default Login;