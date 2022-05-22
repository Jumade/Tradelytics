import { atom } from "recoil";

export interface IPortfolio {
    coins: Array<IPortfolioCoin>,
}
export interface IPortfolioCoin {
    timestamp: number
    symbol: string,
    baseAsset: string,
    quoteAsset: string,
    side: string,
    price: number,
    amount: number,
    cost: number,
    realized_amount: number,
    realized_cost: number,
    open_cost: number,
    realized_pl: number,
    realized_pl_perc: number,
    unrealized_pl: number,
    unrealized_pl_perc: number,
    unrealized_open_cost: number,
    total_pl:number,
    total_pl_perc:number,
}

export const portfolioAtom = atom<IPortfolio>({
    key: "portfolio",
    default: undefined
});

