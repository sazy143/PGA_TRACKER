import React, {Component} from "react";
import ReactDOM from "react-dom";
import {
  HashRouter as Router,
  Switch,
  Route,
  NavLink
} from "react-router-dom";
import '../css/main.css'

//import the pages
import CurrentPage from './CurrentPage/CurrentPage';
import LeaderBoard from './LeaderBoardPage/LeaderBoardPage';
import Future from './FuturePage/FuturePage';
import Predictions from './PredictionsPage/PredictionsPage';
import Past from './PastPage/PastPage';
import Stats from './StatsPage/StatsPage';

//our main component
function Main(){
    return(
        <div>
            <h1 id='logo'>PGA TRACKER</h1>
            <Router>
                <div id='navigation'>
                    <ul>
                        <li className='nav-item'>
                            <NavLink to = "/">Current</NavLink>
                        </li>
                        <li className='nav-item'>
                            <NavLink to = "/leaderboard">Leader Board</NavLink>
                        </li>
                        <li className='nav-item'>
                            <NavLink to = "/future">Future Tournaments</NavLink>
                        </li>
                        <li className='nav-item'>
                            <NavLink to = "/past">Past Tournaments</NavLink>
                        </li>
                        <li className='nav-item'>
                            <NavLink to = "/predictions">Tournament Predictions</NavLink>
                        </li>
                        <li className='nav-item'>
                            <NavLink to = "/stats">Cool Stats</NavLink>
                        </li>
                    </ul>
                </div>
                <div>
                    <Switch>
                        <Route path="/" exact>
                            <CurrentPage/>
                        </Route>
                        <Route path="/leaderboard">
                            <LeaderBoard/>
                        </Route>
                        <Route path="/future">
                             <Future/>
                        </Route>
                        <Route path="/predictions">
                            <Predictions/>
                        </Route>
                        <Route path="/past">
                            <Past/>
                        </Route>
                        <Route path="/stats">
                            <Stats/>
                        </Route>
                    </Switch>

                </div>
            </Router>
        </div>
    );
}
const rootElement = document.getElementById('root');
rootElement ? ReactDOM.render(<Main/>,rootElement) : false;