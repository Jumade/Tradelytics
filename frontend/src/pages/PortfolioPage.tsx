import React from 'react';
import { useRecoilValueLoadable } from 'recoil';
import { portfolioUpdate } from '../actions/PortfolioActions';
import CoinListComponent from '../components/portfolio/CoinListComponent';
import { IPortfolio } from '../state/PortfolioState';
import { Alert, Form ,Stack} from 'react-bootstrap';
import { useAccountActions } from "../actions/AccountActions";
import { IUserSettings, userSettingsAtom } from '../state/AccountState';
import { useRecoilValue } from "recoil";

function PortfolioPage() {
    let portfolio = useRecoilValueLoadable<IPortfolio>(portfolioUpdate);
    let settings = useRecoilValue<IUserSettings | undefined>(userSettingsAtom);
    
    const accountActions = useAccountActions();

    function onChange(event: React.ChangeEvent<HTMLSelectElement>) {
        const target = event.target as typeof event.target & { value: string };
        accountActions.setQuoteAsset(target.value);
    }

    switch (portfolio.state) {
        case 'hasValue':
            return (
                <div>
                    <Stack direction="horizontal" gap={3}>
                    <h3 className="mt-3">Positions:</h3>
                    <div className="ms-auto">Quote Asset:</div>
                    <div className="me-auto ">
                        
                        <Form.Select aria-label="Select quote currency" onChange={onChange} value={settings?.quote_asset_setting} size="sm">
                            <option value="BTC">BTC</option>
                            <option value="USD">USD</option>
                            <option value="EUR">EUR</option>
                        </Form.Select>
                    </div>
                    </Stack>
                    
                    {portfolio.contents.coins && portfolio.contents.coins.length == 0 && (
                        <Alert key="primary" variant="primary">
                            No Positions to show. It may take a new minutes to process trades.
                        </Alert>
                    )}
                    <div>
                        {portfolio.contents.coins.map((coinData) => (
                            <CoinListComponent coin={coinData} quoteAsset={settings?.quote_asset_setting}/>
                        ))}
                    </div>
                </div>
            );
        case 'loading':
          return <div>Loading...</div>;
        case 'hasError':
          throw portfolio.contents;
      }
}
export default PortfolioPage;