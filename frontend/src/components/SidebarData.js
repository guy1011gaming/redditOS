import React from 'react';
import * as Md from "react-icons/md";

export const SidebarData =  [
    {
        title: 'Dashboard',
        icon: <Md.MdDashboard />,
        link: '/'
    },
    {
        title: 'Analytics',
        icon: <Md.MdAnalytics />,
        link: '/analytics'
    },
    {
        title: 'Post',
        icon: <Md.MdAdd />,
        link: '/post'
    }
]