import {Navigate} from "react-router-dom";
import { useRecoilValue } from "recoil";
import {accountLoginRefresh} from "../actions/AccountActions";

export default function PrivateRoute({ children }: { children: JSX.Element }) {
    let userAuth = useRecoilValue(accountLoginRefresh);
    if(userAuth) {
        return children;
    } else {
        return <Navigate to="/login"  />;
    }
};


