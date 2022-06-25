import React, { useState, useEffect } from 'react';
import './Tile.css';
import Post from './Post';

const Tile = () => {
  const [posts, setPosts] = useState([]);
  const [subreddit, setSubreddit] = useState();

  const limit = 15;

  useEffect(() => {
    fetch(`https://www.reddit.com/r/mildlyinfuriating.json?limit=${limit}&include_over_18=on`).then(res => {
      if(res.status !== 200) {
        console.log('ERROR');
        return;
      }

      res.json().then(data => {
        if(data !== null) {
          setPosts(data.data.children);
        }
      });
    })
  }, [subreddit]);

  return (
    <div className='Tile'>
        <div className='TileMid'>
          <h1>Your recent posts.</h1>
          {
            (posts !== null) ? posts.map((post, index) => <Post key={index} post={post.data}/>) : ''
          }
        </div>
        <div className='TileRight'>
          <h1>Suggestions.</h1>
          <div className='TileRightBox'>
            <p className='rightTileTitle'>check out these subreddits</p>
            
          </div>
          <div className='TileRightBox'>
            <p className='rightTileTitle'>chart</p>
          </div>
        </div>
    </div>
  )
}

export default Tile;