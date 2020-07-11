import React from 'react';
import { List, Header } from "semantic-ui-react";

export const Shops = ({ shops }) => {
  return (
    <List>
      Shops List
      {shops.map(shop => {
        return (
          <List.Item key={shop.name}>
            <Header>{shop.name} : {shop.description}</Header>
            <div>{shop.hours} |{shop.address} |{shop.phone}|{shop.website}|{shop.price_level}</div>
          </List.Item>
        )
      })}
    </List>
  )
}