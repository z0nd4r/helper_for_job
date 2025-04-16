// export const refreshTokenInterval = 899000; // 14 minutes and 59 seconds in milliseconds

export const ENDPOINTS = {
    login: `http://127.0.0.1:8000/auth/login`,
    register: `http://127.0.0.1:8000/auth/register`,
    channels: `http://127.0.0.1:8000/channels`, // GET, POST
    channelDetail: (channelId) => `/channels/${channelId}`, // GET, PUT, DELETE
    channelInvite: (channelId) => `/channels/${channelId}/invite`, // POST
    channelMessages: (channelId) => `/channels/${channelId}/messages`,  // GET, POST
    refreshToken: `http://127.0.0.1:8000/auth/refresh`,
    delete_cookie: `http://127.0.0.1:8000/auth/delete_cookie`,
};

