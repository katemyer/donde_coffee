import React from 'react';
import { List, Header } from "semantic-ui-react";

export const Reviews = ({ reviews }) => {
  return (
    <List>
      Reviews List
      {reviews.map(review => {
        return (
          <List.Item key={shop.name}>
            <Header>{review.description} : {review.shop_id}</Header>
          </List.Item>
        )
      })}
    </List>
  )
}