import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/main.scss';
import React from 'react';
// import ReactDOM from 'react-dom';
import { createRoot } from "react-dom/client";
import NavBar from './components/navbar';
import HomePage from './components/home';
import SignUpPage from './components/signup';
import LoginPage from './components/login';
import CommunityPage from './components/community';
import ProfilePage from './components/profile';
import LibraryPage from './components/library';
import {
    BrowserRouter as Router,
    Routes,
    Route,
} from 'react-router-dom';

// changing div className from app to container makes the navbar not fill up the screen

const App = () => {

    return (
        <Router>
        <div className='app'> 
            <div className='gradient-body'>
                <div className='gradient'></div>
            </div>
            <NavBar/>
            {/* <Switch> */}
                {/* <Route path='/' exact component={HomePage}/> */}
                {/* <Route path='/signup' exact component={SignUpPage}/> */}
                {/* <Route path='/login' exact component={LoginPage}/> */}
                {/* <Route path='/community' exact component={CommunityPage}/> */}
                {/* <Route path='/logout' exact component={Logout}/> */}
            {/* </Switch> */}
            <Routes>
                <Route path='/' element={<HomePage/>}/>
                <Route path='/signup' element={<SignUpPage/>}/>
                <Route path='/login' element={<LoginPage/>}/>
                <Route path='/community' element={<CommunityPage/>}/>
                <Route path='/library' element={<LibraryPage/>}/>
                <Route path='/profile' element={<ProfilePage/>}/>
            </Routes>
        </div>
        </Router>
    );
}

// ReactDOM.render(<App/>, document.getElementById('root'));
const rootElement = document.getElementById("root");
const root = createRoot(rootElement);
root.render(<App/>);