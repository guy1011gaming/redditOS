import React from 'react';
import './Sidebar.css';
import { SidebarData } from './SidebarData';
import logo from '../images/logo_sketch.png';
import userpicture from '../images/profilepic.png';

const Sidebar = () => {
    const username = 'AverageRedditUser';
    const profilepicture = userpicture;

    return (
    <div className='Sidebar'>
        <div className='neptune'>
            <img src={logo} alt='neptune logo' />
            <p>neptune webapp.</p>
        </div>
        <div className='profile'>
            <div className='SidebarHead'>
                <div className='SidebarProfilePicture'>
                    <img src={profilepicture} alt='profile pic' />
                </div>
                <p>@{username}</p>
            </div>
        </div>
        <ul className='SidebarUL'>
            {SidebarData.map((val, key) => {
                return (
                    <li
                    key={key}
                    className='SidebarLI'
                    id={window.location.pathname === val.link ? "active" : ""}
                    onClick={() => {
                        window.location.pathname = val.link
                    }}>
                        <div id='icon'>{val.icon}</div>
                        <div id='title'>{val.title}</div>
                    </li>
                );
            })}
        </ul>
    </div>
    )
}

export default Sidebar