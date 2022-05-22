import React, { useState } from 'react';
import { Alert, Button, Collapse, Form, Stack } from 'react-bootstrap';
import { useRecoilValue } from 'recoil';
import { useAccountActions } from '../actions/AccountActions';
import { IUserSettings, userSettingsAtom } from '../state/AccountState';


export default function AccountSettingsPage() {
    let settings = useRecoilValue<IUserSettings | undefined>(userSettingsAtom);
    const [open, setOpen] = useState(false);
    const accountActions = useAccountActions();
    

    function handleUpdate(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault();
        const target = event.target as typeof event.target & {
            name: { value: string };
            exchange_id: { value: string };
            apikey: { value: string };
            apisecret: { value: string };
            id: { value: string };
          };
          accountActions.updateExchange(+target.id.value, target.name.value, target.exchange_id.value, target.apikey.value, target.apisecret.value)

    }

    function handleAdd(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault();
        const target = event.target as typeof event.target & {
            name: { value: string };
            exchange_id: { value: string };
            apikey: { value: string };
            apisecret: { value: string };
           
          };
          setOpen(false)
          accountActions.addExchange(target.name.value, target.exchange_id.value, target.apikey.value, target.apisecret.value)
    }

    function handleDelete(id: number) {
          accountActions.removeExchange(id)
    }

    return (
        <div>
            <div>
                <h2>API Keys:</h2>
                {settings?.exchanges && settings?.exchanges.length == 0 && (
                    <Alert key="primary" variant="primary">
                    You have no Exchanges configured.
                    </Alert>
                )}
                {settings?.exchanges.map((exchange) => (
                    <div className="shadow-sm p-3 mb-5 bg-light rounded">
                    <Form onSubmit={handleUpdate}>
                        <h3>{exchange.exchange_id}</h3>
                        <Form.Group className="mb-3" controlId="name">
                            <Form.Label>Name</Form.Label>
                            <Form.Control type="text" placeholder="Name" defaultValue={exchange?.name} required/>
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="apikey">
                            <Form.Label>API Key</Form.Label>
                            <Form.Control type="text" placeholder="API Key" defaultValue={exchange?.apikey} required/>
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="apisecret">
                            <Form.Label>API Secret</Form.Label>
                            <Form.Control type="text" placeholder="API Secret" defaultValue={exchange?.apisecret} required/>
                        </Form.Group>
                        <Form.Control name="id" value={exchange.id} type="hidden" />
                        <Form.Control name="exchange_id" value={exchange.exchange_id} type="hidden" />
                        <Stack direction="horizontal" gap={3}>
                            <Button variant="primary" type="submit">
                                Update
                            </Button>
                            <div className="vr" />
                            <Button variant="danger" onClick={() => handleDelete(exchange.id)}>Delete</Button>
                        </Stack>
                    </Form>
                    </div>
                ))}


                
                <Button
                        onClick={() => setOpen(!open)}
                        aria-controls="example-collapse-text"
                        aria-expanded={open}
                    >
                        Add Exchange
                    </Button>

                <Collapse in={open}>
                    
                    <div className="shadow-sm p-3 mb-5 bg-light rounded">
                    <h2>Add New Exchange</h2>
                    <Form onSubmit={handleAdd}>

                        <Form.Group className="mb-3" controlId="name">
                            <Form.Label>Name</Form.Label>
                            <Form.Control type="text" placeholder="Name" required/>
                        </Form.Group>

                        
                        <Form.Group className="mb-3" controlId="exchange_id">
                        <Form.Label>Exchange</Form.Label>
                            <Form.Select aria-label="Select Exchange">
                                <option>Open this select menu</option>
                                <option value="binance">Binance</option>
                                <option value="kraken">Kraken</option>
                            </Form.Select>
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="apikey">
                            <Form.Label>API Key</Form.Label>
                            <Form.Control type="text" placeholder="API Key" required/>
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="apisecret">
                            <Form.Label>API Secret</Form.Label>
                            <Form.Control type="text" placeholder="API Secret" required/>
                        </Form.Group>

                        <Button variant="primary" type="submit">
                            Add
                        </Button>
                    </Form>
                    </div>
                </Collapse>
                
                
            </div>
        </div>
    );
}