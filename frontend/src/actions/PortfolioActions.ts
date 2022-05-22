import http from "../http-common";
import { selector } from "recoil";
import { authUserAtom, userSettingsAtom } from '../state/AccountState';
import { IPortfolio, IPortfolioCoin } from "../state/PortfolioState";

export const portfolioUpdate = selector<IPortfolio>({
    key: 'portfolioUpdate',
    get: async ({ get }) => {
        let userAuth = get(authUserAtom);
        if (userAuth == undefined) {
            return { coins: [] };
        }
        let usersettings = get(userSettingsAtom);
        try {
            var url = `/coinlist/portfolio/${usersettings?.quote_asset_setting}`;
            const response = await http.get<Array<IPortfolioCoin>>(url, {
                headers: {
                    'Authorization': `Bearer ${userAuth.access_token}`
                }
            })
            let portfolio: IPortfolio = { coins: response.data }
            return portfolio
        } catch (error) {
            console.error(error);
            return { coins: [] };
        }
    },
});


