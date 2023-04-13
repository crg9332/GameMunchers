import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../auth';
import TextField from "@mui/material/TextField";


const LoggedinHome = () => {
    return (
        <div className='store home'>
            <h1 className='heading'>Store</h1>
            <Link to='/community' className='btn btn-primary btn-lg'>Community</Link>
        </div>
    );
}

const LoggedoutHome = () => {
    return (
        <div className='home container'>
            <h1 className='heading'>Store</h1>
            <Link to='/signup' className='btn btn-primary btn-lg'>Sign Up</Link>
        </div>
    );
}

const HomePage = () => {

    const [logged] = useAuth();

    const [games, setGames] = React.useState([])

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            if (e.target.value === '') {
                return
            } else {
                // console.log(e.target.value)

                const body = {
                    title: e.target.value
                }

                const options = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(body)
                }

                fetch('/api/search/game', options)
                    .then(response => response.json())
                    .then(data => {
                        // console.log(data)
                        // format data into displayable html format
                        if (!data.error) {
                            // console.log(data)
                            setGames(data)
                        }
                    })
                    .catch(error => {
                        console.log(error);
                    });
            }
        }
    }

    // return (
    //     <div>
    //         {logged ? <LoggedinHome /> : <LoggedoutHome />}
    //     </div>
    // );
    // searchable page with games
    return (
        <div className="main">
            {/* <h1>React Search</h1> */}
            <div className="search">
                {/* <TextField
                    // id="search"
                    // variant="outlined"
                    // fullWidth
                    className={StyleSheet.search}
                    label="Search"
                    // color='primary'
                /> */}
                <input className='input-search' type="text" placeholder="Search Games" onKeyUp={handleKeyPress} />
            </div>
            <div className="results">
                {games.map((game) => (
                    <div className="about">
                        {/* make it so animations to the about border gradient are forced to finish after a user stops hovering */}
                        <div className="game">{game.gametitle}</div>
                        <div className="gameReleaseDate">{game.releasedate}</div>
                        <div className="gameplatform">{game.platformtype}</div>
                        {/* <div className="gameprice">{game.price}</div> */}
                        <div className="gamerating" style={{ color: game.avgrating === 'N/A' ? 'white' : `rgb(${255 - game.avgrating * 50}, ${game.avgrating * 50}, 0)` }}>{game.avgrating}</div>
                        <div className="gameDevs">{game.developer}</div>
                        <div className="gamePub">{game.publisher}</div>
                        <div className="gamePlayTime">{game.playtime}</div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default HomePage;