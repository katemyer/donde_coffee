import React from 'react';
import { List, Header } from "semantic-ui-react";

export const Users = ({ users }) => {
  return (
    <List>
      Users List
      {users.map(user => {
        return (
          <List.Item key={user.name}>
            <Header>{user.name} : {user.email}</Header>
          </List.Item>
        )
      })}
    </List>
  )
}