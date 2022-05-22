import http from "../http-common";
import { selector, useRecoilState, useSetRecoilState } from "recoil";
import { authUserAtom, IUserAuth, IUserSettings, userSettingsAtom } from '../state/AccountState';
import { useNavigate } from "react-router-dom";

export const accountLoginRefresh = selector<IUserAuth | undefined>({
    key: 'accountLoginRefresh',
    get: async ({get}) => {
        const token = window.localStorage.getItem('refreshToken');
        if (token) {
            window.localStorage.removeItem('refreshToken');
            try {
                const response = await http.get<IUserAuth>("/user/refresh", {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                let user = response.data as IUserAuth
                console.log(response.data);
                localStorage.setItem('refreshToken', response.data.refresh_token);
                return user
            } catch (error) {
                console.error(error);
            }
        }
        return undefined
    },
});

export const settingsUser = selector<IUserSettings | undefined>({
    key: 'settingsUser',
    get: async ({get}) => {
        console.log("settingsUser");
        let userAuth = get(authUserAtom);
        try {
            const response = await http.get<IUserSettings>("/user/settings", {
                headers: {
                    'Authorization': `Bearer ${userAuth?.access_token}`
                }
            })
            let user = response.data as IUserSettings
            console.log(response.data);
            return user
        } catch (error) {
            console.error(error);
        }
        return undefined
    },
});


export function useAccountActions() {
    let [userAuth, setAuthUser] = useRecoilState<IUserAuth|undefined>(authUserAtom);
    let setUserSettings = useSetRecoilState<IUserSettings|undefined>(userSettingsAtom);
    let navigate = useNavigate();

    return {
        login,
        register,
        signout,
        addExchange,
        updateExchange,
        removeExchange,
        setQuoteAsset
    }
    function setQuoteAsset(name: string) {
        http.post<IUserSettings>("/user/quote",
            { "name": name },
            {headers: {
                'Authorization': `Bearer ${userAuth?.access_token}`
            }})
            .then((res: any) => {
                let settings = res.data as IUserSettings

                setUserSettings(settings);
            })
            .catch((err: any) => {
                console.log(err);
            });
    }

    function addExchange(name: string, exchange_id: string, apikey: string, apisecret: string) {
        http.post<IUserSettings>("/user/exchange",
            { "name": name, "exchange_id": exchange_id, "apikey": apikey, "apisecret": apisecret },
            {headers: {
                'Authorization': `Bearer ${userAuth?.access_token}`
            }})
            .then((res: any) => {
                let settings = res.data as IUserSettings

                setUserSettings(settings);
            })
            .catch((err: any) => {
                console.log(err);
            });
    }

    function removeExchange(id: number) {
        var url = `/user/exchange-update/${id}`;
        http.delete<IUserSettings>(url,
            {headers: {
                'Authorization': `Bearer ${userAuth?.access_token}`
            }})
            .then((res: any) => {
                let settings = res.data as IUserSettings

                setUserSettings(settings);
            })
            .catch((err: any) => {
                console.log(err);
            });
    }
    

    function updateExchange(id: number, name: string, exchange_id: string, apikey: string, apisecret: string) {
        var url = `/user/exchange-update/${id}`;
        http.put<IUserSettings>(url,
            {"name": name, "exchange_id": exchange_id, "apikey": apikey, "apisecret": apisecret },
            {headers: {
                'Authorization': `Bearer ${userAuth?.access_token}`
            }})
            .then((res: any) => {
                let settings = res.data as IUserSettings

                setUserSettings(settings);
            })
            .catch((err: any) => {
                console.log(err);
            });
    }

    function login(user: string, password: string) {
        http.post<IUserAuth>("/user/login", { "username": user, "password": password })
            .then((res: any) => {
                let user = res.data as IUserAuth

                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('refreshToken', user.refresh_token);
                setAuthUser(user);
                navigate("/");
            })
            .catch((err: any) => {
                console.log("login error");
                console.log(err);
            });
    }

    function register(user: string, password: string) {
        http.post("/user/register", { "username": user, "password": password })
            .then((res: any) => {
                console.log(res.data);
            })
            .catch((err: any) => {
                console.log(err);
            });
    };

   
    function signout() {
        localStorage.removeItem('refreshToken');
        setAuthUser(undefined);
        navigate("/login");
    }
}

