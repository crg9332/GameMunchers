import React, { useState } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useAuth } from '../auth';

const SignUpPage = () => {
    const [logged] = useAuth();

    // if logged in, redirect to home page
    if (logged) {
        window.location.href = '/';
    }


    const { register, watch, handleSubmit, reset, formState: { errors } } = useForm();
    const [showSuccess, setShowSuccess] = useState(false);
    const [showFailure, setShowFailure] = useState(false);
    const [serverResponse, setServerResponse] = useState("");

    const submitForm = (data) => {

        if (data.password !== data.confirmPassword) {
            alert("Passwords don't match");
            return;
        }

        // console.log(data);

        const body = {
            username: data.username,
            email: data.email,
            password: data.password,
            firstname: data.firstName,
            lastname: data.lastName
        }

        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        }

        fetch('/api/auth/signup', requestOptions)
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    setServerResponse(data.message);
                    setShowSuccess(true);
                    setShowFailure(false);
                    reset();
                } else {
                    alert(data)
                    setServerResponse(data.error);
                    setShowSuccess(false);
                    setShowFailure(true);
                }
            })
            .catch(error => {
                console.log(error);
                setServerResponse("Something went wrong");
                setShowSuccess(false);
                setShowFailure(true);
            });
    }


    return (
        <div className='container'>
            <div className="form">
                {showSuccess ?
                    <>
                        <Alert variant="success" onClose={() => setShowSuccess(false)} dismissible>
                            {serverResponse}
                        </Alert>
                    </>
                    : null
                }
                {showFailure ?
                    <>
                        <Alert variant="danger" onClose={() => setShowFailure(false)} dismissible>
                            {serverResponse}
                        </Alert>
                    </>
                    : null
                }
                <h1 className='heading'>Sign Up</h1>
                <form>
                    <Form.Group className="mb-3" controlId="formBasicUsername">
                        <Form.Label>Username</Form.Label>
                        <Form.Control type="username"
                            placeholder="Enter username"
                            {...register("username", { required: true, maxLength: 25 })}
                        />
                        {errors.username?.type === "required" && <p style={{ color: "red" }}><small>Username is required</small></p>}
                    </Form.Group>

                    {/* Add inputs for an optional first and last name */}
                    <Form.Group className="mb-3" controlId="formBasicFirstName">
                        <Form.Label>First Name</Form.Label>
                        <Form.Control type="firstName"
                            placeholder="Enter first name"
                            {...register("firstName", { required: false, maxLength: 25 })}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicLastName">
                        <Form.Label>Last Name</Form.Label>
                        <Form.Control type="lastName"
                            placeholder="Enter last name"
                            {...register("lastName", { required: false, maxLength: 25 })}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Label>Email address</Form.Label>
                        <Form.Control type="email"
                            placeholder="Enter email"
                            {...register("email", { required: true, pattern: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i, maxLength: 80 })}
                        />
                        {errors.email?.type === "required" && <p style={{ color: "red" }}><small>Email is required</small></p>}
                        {errors.email?.type === "pattern" && <p style={{ color: "red" }}><small>Email is invalid</small></p>}
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicPassword">
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password"
                            placeholder="Password"
                            {...register("password", { required: true, minLength: 8 })}
                        />
                        {errors.password?.type === "required" && <p style={{ color: "red" }}><small>Password is required</small></p>}
                        {errors.password?.type === "minLength" && <p style={{ color: "red" }}><small>Password must be at least 8 characters</small></p>}
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Confirm Password</Form.Label>
                        <Form.Control type="password"
                            placeholder="Password"
                            {...register("confirmPassword", { required: true, minLength: 8 })}
                        />
                        {watch("password") !== watch("confirmPassword") && <p style={{ color: "red" }}><small>Passwords do not match</small></p>}
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicSubmit">
                        <Button as='sub' variant='primary' onClick={handleSubmit(submitForm)}>
                            Submit
                        </Button>
                    </Form.Group>

                    <Form.Group>
                        <small>Already have an account? <Link to='/login'>Login</Link></small>
                    </Form.Group>


                </form>

            </div>
        </div>
    );
}

export default SignUpPage;