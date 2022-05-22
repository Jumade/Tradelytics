import React from 'react';
import {Button, Form} from "react-bootstrap";
import {useAccountActions} from "../actions/AccountActions";

function LoginPage() {
    const accountActions = useAccountActions();
    
    function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault();
        const target = event.target as typeof event.target & {
            username: { value: string };
            password: { value: string };
          };

        let username = target.username.value;
        let password = target.password.value;

        accountActions.login(username, password);
    }

    return (
        <Form onSubmit={handleSubmit}>
            <h3>Login</h3>
            <Form.Group className="mb-3" controlId="username">
                <Form.Label>Username</Form.Label>
                <Form.Control type="username" placeholder="Enter username" required/>
            </Form.Group>

            <Form.Group className="mb-3" controlId="password">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password" required/>
            </Form.Group>

            <Button variant="primary" type="submit">
                Submit
            </Button>
        </Form>
    );
}
export default LoginPage;