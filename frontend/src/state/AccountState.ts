import { atom } from "recoil";
import { accountLoginRefresh, settingsUser } from "../actions/AccountActions";

export interface IUserAuth {
    refresh_token: string,
    access_token: string
}

export const authUserAtom = atom<IUserAuth | undefined>({
    key: "auth",
    default: accountLoginRefresh
});

export const userSettingsAtom = atom<IUserSettings | undefined>({
    key: "userSettings",
    default: settingsUser
});


export interface IUserSettings {
    name: string,
    quote_asset_setting: string
    exchanges: Array<IExchangeSettings>
}

export interface IExchangeSettings {
    id: number,
    user_id: number,
    name: string,
    exchange_id: string,
    apikey: string,
    apisecret: string,
    active: boolean,
    valid: boolean
}



