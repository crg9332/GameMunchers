import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth, logout } from '../auth';
import './_navbar.scss';

const LoggedIntLinks = () => {
    const currentRoute = useLocation().pathname;
    return (
        <div className="sidenav-nav">
            <Link 
            className={`my-nav-link ${currentRoute === '/' ? 'active' : ''}`}
            to="/">Store</Link>
            <Link 
            className={`my-nav-link ${currentRoute === '/library' ? 'active' : ''}`}
            to="/library">Library</Link>
            <Link 
            className={`my-nav-link ${currentRoute === '/community' ? 'active' : ''}`} 
            to="/community">Community</Link>
            <Link 
            className={`my-nav-link ${currentRoute === '/profile' ? 'active' : ''}`} 
            to="/profile">Profile</Link>
            <Link className="my-nav-link" id='logout' to="/login" onClick={() => { logout() }}>Log Out</Link>
        </div>
    );
}

const LoggedOutLinks = () => {
    const currentRoute = useLocation().pathname;
    return (
        <div className="sidenav-nav">
            <Link 
            className={`my-nav-link ${currentRoute === '/' ? 'active' : ''}`}
            to="/">Store</Link>
            {/* <Link 
            className={`my-nav-link ${currentRoute === '/login' ? 'active' : ''}`}
            to="/login">Login/Signup</Link> */}
            {/* set active if currentRoute is /login or /signup */}
            <Link
            className={`my-nav-link ${currentRoute === '/login' || currentRoute === '/signup' ? 'active' : ''}`}
            to="/login">Login/Signup</Link>
            {/* <Link 
            className={`my-nav-link ${currentRoute === '/community' ? 'active' : ''}`}
            to="/signup">Sign Up</Link> */}
        </div>
    );
}

const NavBar = () => {

    const [logged] = useAuth();

    return (
        <nav className="sidenav">
            {/* <Link className="my-navbar-brand" to="/"><img src="img/logo.svg" alt="logo" />GameMunchers</Link> */}
            {/* make the logo 48x48px */}
            <Link className="my-navbar-brand" to="/"><img src="img/logo.svg" alt="logo" width={'48px'} />GameMunchers</Link>
            {logged ? <LoggedIntLinks /> : <LoggedOutLinks />}
        </nav>
    );
}

// const NavBar = () => {

//     const [logged] = useAuth();

//     return (
//         <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
//             <div className="container-fluid">
//                 {/* <a className="navbar-brand" href="#">GameMunchers</a> */}
//                 <Link className="navbar-brand" to="/">GameMunchers</Link>
//                 <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
//                     <span className="navbar-toggler-icon"></span>
//                 </button>
//                 <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
//                     {logged ? <LoggedIntLinks /> : <LoggedOutLinks />}
//                 </div>
//             </div>
//         </nav>
//     );
// }

// make a vertical navbar
// const NavBar = () => {

//     const [logged] = useAuth();

//     const [window, setWindow] = useState(false);

//     let openClose = () => {
//         if (window === false) {
//             setWindow(true);
//         } else {
//             setWindow(false);
//         }
//     };
//     return (
//         <nav className="navbar-menu" style={{ width: window === false ? 250 : 60 }}>
//             <div className="burger" onClick={() => openClose()}>
//                 <img src="img/menu.svg" alt="burger" />
//             </div>
//             <div className="navbar-items">
//                 {/* <div className="navbar-logo">
//                     <img src="img/logo.svg" alt="logo" />
//                 </div> */}
//                 <ul className="navbar-items">
//                     <li className="navbar__li">
//                         <Link to="/" className="navbar-link">
//                             <img
//                                 src="img/store.svg"
//                                 alt="store"
//                                 style={{ paddingLeft: window === false ? 27 : 17 }}
//                             />
//                             <span
//                                 className="link-name"
//                                 style={{ display: window === false ? "inline-block" : "none" }}
//                             >
//                                 Store
//                             </span>
//                         </Link>
//                     </li>
//                     <li className="navbar__li">
//                         <Link to="/findfriends" className="navbar-link">
//                             <img
//                                 src="img/community.svg"
//                                 alt="community"
//                                 style={{ paddingLeft: window === false ? 27 : 17 }}
//                             />
//                             <span
//                                 className="link-name"
//                                 style={{ display: window === false ? "inline-block" : "none" }}
//                             >
//                                 Community
//                             </span>
//                         </Link>
//                     </li>
//                     <li className="navbar__li">
//                         <Link to="/" className="navbar-link" onClick={() => { logout() }}>
//                             <img
//                                 src="img/logout.svg"
//                                 alt="logout"
//                                 style={{ paddingLeft: window === false ? 27 : 17 }}
//                             />
//                             <span
//                                 className="link-name"
//                                 style={{ display: window === false ? "inline-block" : "none" }}
//                             >
//                                 Logout
//                             </span>
//                         </Link>
//                     </li>
//                 </ul>
//             </div>
//         </nav>
//     );
// }

// const NavBar = () => {
//     const [logged] = useAuth();

//     // set li to the correct links based on if the user is logged in or not
//     let li = [];
//     if (logged) {
//         li = [
//             ["Store", "img/store.svg", "/"],
//             ["Community", "img/community.svg", "/findfriends"],
//             ["Logout", "img/logout.svg", "/"],
//         ];
//     } else {
//         li = [
//             ["Store", "img/store.svg", "/"],
//             ["Sign Up", "img/signup.svg", "/signup"],
//             ["Login", "img/login.svg", "/login"],
//         ];
//     }

//     const [window, setWindow] = useState(false);

//     let openClose = () => {
//       if (window === false) {
//         setWindow(true);
//       } else {
//         setWindow(false);
//       }
//     };
//     return (
//       <nav className="navbar-menu" style={{ width: window === false ? 250 : 60 }}>
//         <div className="burger" onClick={() => openClose()}>
//           <img src="img/menu.svg" alt="burger" />
//         </div>
//         <ul className="navbar__list">
//           {li.map((item, i) => (
//             <div className="navbar__li-box" key={i}>
//               <img
//                 src={item[1]}
//                 alt={item[1]}
//                 style={{ paddingLeft: window === false ? 27 : 17 }}
//               />
//               <li
//                 className="navbar__li"
//                 style={{ display: window === false ? "inline-block" : "none" }}
//               >
//                 {item[0]}
//               </li>
//             </div>
//           ))}
//         </ul>
//       </nav>
//     );
//   };


export default NavBar;