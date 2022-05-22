import { atom } from "recoil";

export interface IAlert {
    message: string,
    type: string
}

export const alertAtom = atom<IAlert | null>({
    key: 'alert',
    default: null
});

