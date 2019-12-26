import React, {Component} from "react";
import ReactDOM from "react-dom";
import TableMaker from "../Components/TableMaker/TableMaker/TableMaker.js/index.js.js.js";
const data = require('../jsonFiles/current.json');

class CurrentPage extends Component {
    constructor(){
        super();
        
        this.state = {
            tournament: null
        };
    }
    
    componentDidMount(){
        try{
           
            this.setState({
                tournament: data.tournament
            });
        }catch(err){
            console.log(err);
        }
        
        
    }
    
    render(){

        return(
            <div className='page-content'>
                <h1>Current Tournament: {this.state.tournament}</h1>
                <TableMaker data ={data}/>
            </div>
        ); 
    }
    
}

export default CurrentPage;