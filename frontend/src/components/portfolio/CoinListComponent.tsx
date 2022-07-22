import React from 'react';
import { Col, Container, Row } from 'react-bootstrap';
import { IPortfolioCoin } from '../../state/PortfolioState';
interface ICoinListComponentProps {
    coin: IPortfolioCoin
  }

function CoinListComponent(props: ICoinListComponentProps) {
    return <Container>
            <Row className="shadow-sm p-1 mb-3 bg-light rounded">
              <Col>{props.coin.baseAsset}</Col>
              <Col></Col>
              <Col><div className="text-muted">Unrealized P/L:</div>
                <div className={props.coin.unrealized_pl >= 0 ? "text-success" : "text-danger"}>{Math.round(props.coin.unrealized_pl*10000)/10000} ({Math.round(props.coin.unrealized_pl_perc*100)}%)</div></Col>
              <Col><div className="text-muted">Realized P/L:</div>
                  <div className={props.coin.realized_pl >= 0 ? "text-success" : "text-danger"}>{Math.round(props.coin.realized_pl*10000)/10000} ({Math.round(props.coin.realized_pl_perc*100)}%)</div></Col>
              <Col><div className="text-muted">Total P/L:</div>
                  <div className={props.coin.total_pl >= 0 ? "text-success" : "text-danger"}>{Math.round(props.coin.total_pl*10000)/10000} ({Math.round(props.coin.total_pl_perc*100)}%)</div></Col>
            </Row>
          </Container>
}

export default CoinListComponent;

