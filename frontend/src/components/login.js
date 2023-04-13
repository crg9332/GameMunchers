import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { login } from '../auth';
import { useNavigate } from 'react-router-dom';


const LoginPage = () => {

    const { register, handleSubmit, reset, formState: { errors } } = useForm();

    const navigate = useNavigate();


    const loginUser = (data) => {
        console.log("login user");
        console.log(data);

        const body = {
            username: data.username,
            password: data.password
        }

        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        }

        fetch('/api/auth/login', requestOptions)
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    console.log(data);
                    login(data.access_token);
                    navigate('/');
                    // localStorage.setItem('token',data.token);
                    // localStorage.setItem('user',data.user);
                    // window.location.href = '/home';
                } else {
                    alert("Error: " + data.error)
                }
            })
            .catch(error => {
                console.log(error);
                alert("Something went wrong")
            }
            );
    }
    return (
        <div className='my-container'>
            <div className="form-box">
                <form>
                    <h1 className='heading'>Login</h1>
                    <div className="field-login">
                        <input className='input-login' type="text" autocomplete="off" spellcheck="false" name="username" placeholder="" {...register("username", { required: true, maxLength: 25 })} required />
                        {errors.username?.type === "required" && <style>{'.field-login:nth-child(even) .label-login {color: red;}.field-login:nth-child(even) {border-bottom: 2px dashed red;}'}</style>}
                        <label className='label-login' htmlFor="username">Username</label>
                    </div>

                    <div className="field-login">
                        <input className='input-login' type="password" name="password" placeholder="" {...register("password", { required: true, maxLength: 25 })} required />
                        {errors.password?.type === "required" && <style>{'.field-login:nth-child(odd) .label-login {color: red;}.field-login:nth-child(odd) {border-bottom: 2px dashed red;}'}</style>}
                        <label className='label-login' htmlFor="password">Password</label>
                    </div>

                    <div className="submit">
                        {/* <Button as='sub' variant='primary' onClick={handleSubmit(loginUser)}>
                            Login
                        </Button> */}
                        <input type="submit" className='submit-login' value="Login" onClick={handleSubmit(loginUser)} />
                    </div>

                    <div className="signup-text">
                        <small>Don't have an account? <Link to='/signup'>Sign Up</Link></small>
                    </div>
                </form>
            </div>
        </div>
    );
    // return (
    //     <div className='my-container'>
    //         <div className="form">
    //             <h1 className='heading'>Login</h1>
    //             <form>
    //                 <Form.Group className="mb-3" controlId="formBasicUsername">
    //                     <Form.Label>Username</Form.Label>
    //                     <Form.Control type="username"
    //                         placeholder="Enter username"
    //                         name="username"
    //                         {...register("username", { required: true, maxLength: 25 })}
    //                     />
    //                     {errors.username?.type === "required" && <p style={{ color: "red" }}><small>Please enter a username</small></p>}
    //                 </Form.Group>

    //                 <Form.Group className="mb-3" controlId="formBasicPassword">
    //                     <Form.Label>Password</Form.Label>
    //                     <Form.Control type="password"
    //                         placeholder="Enter password"
    //                         name="password"
    //                         {...register("password", { required: true, maxLength: 25 })}
    //                     />
    //                     {errors.password?.type === "required" && <p style={{ color: "red" }}><small>Please enter a password</small></p>}
    //                 </Form.Group>

    //                 <Form.Group className="mb-3" controlId="formBasicSubmit">
    //                     <Button as='sub' variant='primary' onClick={handleSubmit(loginUser)}>
    //                         Login
    //                     </Button>
    //                 </Form.Group>

    //                 <Form.Group>
    //                     <small>Don't have an account? <Link to='/signup'>Sign Up</Link></small>
    //                 </Form.Group>

    //             </form>
    //         </div>
    //     </div>
    // );
}

export default LoginPage;