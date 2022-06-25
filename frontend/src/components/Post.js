import React from 'react';
import './Post.css';

const Post = (props) => {
  return (
    <>
    <div className='Post'>
        <p className='postSubredditDate'>
            {props.post.subreddit_name_prefixed} - {(new Date(props.post.created_utc * 1000)).getHours()}h {(new Date(props.post.created_utc * 1000)).getMinutes()}m ago
        </p>
        {
            ((props.post.thumbnail).startsWith('https://')) ? <div className='thumbnail'><img src={props.post.thumbnail} alt='thumbnail'/></div> : ''
        }
        <a href={'https://www.reddit.com/' + props.post.permalink} target='_blank' rel='noreferrer'>
            <p className='postTitle'>{props.post.title}</p>
        </a>
    </div>
    </>
  )
}

export default Post;