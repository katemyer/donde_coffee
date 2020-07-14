import React, { Component, header } from 'react';
import axios from 'axios';

export default class Registration extends Component {
  constructor(props) {
    super(props);

    this.state = {
      email: "",
      name: "",
      password: "",
      registrationErrors: ""
    }

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({
      [event.target.name]: event.target.value
    })
  }

  handleSubmit(event) {
    
    axios.post("http://localhost:5000/signup", {
      user: {
        email: this.state.email,
        name: this.state.name,
        password: this.state.password
      }
    },
    // MAKE SURE THIS NEXT LINE DOESN'T BREAK THINGS
    // { withCredentials: true }
    ).then(response => {
      console.log('registration res', response);
    }).catch(error => {
      console.log("registration error", error);
    })
    event.preventDefault();
  }

  render() {
    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          <input
          type="email"
          name="email"
          placeholder="Email"
          value={this.state.email}
          onChange={this.handleChange} required />
          <input
          type="name"
          name="name"
          placeholder="Name"
          value={this.state.name}
          onChange={this.handleChange} required />
          <input
          type="password"
          name="password"
          placeholder="Password"
          value={this.state.password}
          onChange={this.handleChange} required />

          <button type="submit">Register</button>
        </form>
      </div>);
  }
}