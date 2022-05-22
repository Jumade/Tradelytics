import {Resetter, SetterOrUpdater, useResetRecoilState, useSetRecoilState} from "recoil";
import {alertAtom, IAlert} from "../state/AlertState";

class AlertActions {
    private setAlert: SetterOrUpdater<IAlert | null>;
    private resetAlert: Resetter;

    constructor () {
        this.setAlert = useSetRecoilState(alertAtom);
        this.resetAlert = useResetRecoilState(alertAtom);
    }

    success(message: string) {
        this.setAlert({ message, type: 'alert-success' })
    }

    error(message: string) {
        this.setAlert({ message, type: 'alert-danger' })
    }

    clear() {
        this.resetAlert();
    }
}

export default new AlertActions();