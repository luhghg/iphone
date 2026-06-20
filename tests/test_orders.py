async def test_create_order(client, auth_headers, product_variant):
    await client.post("/cart/items", json={"product_variant_id": product_variant["id"], "quantity": 2}, headers=auth_headers)
    response = await client.post("/orders", json={"delivery_address": "Kyiv, Khreshchatik 7"}, headers=auth_headers)
    assert response.status_code == 201
    assert "id" in response.json()


async def test_create_order_empty_cart(client, auth_headers):
    response = await client.post("/orders", json={"delivery_address": "Kyiv, Khreshchatik 7"}, headers=auth_headers)
    assert response.status_code == 400


async def test_get_my_orders(client, auth_headers, product_variant):
    await client.post("/cart/items", json={"product_variant_id": product_variant["id"], "quantity": 2}, headers=auth_headers)
    await client.post("/orders", json={"delivery_address": "Kyiv, Khreshchatik 7"}, headers=auth_headers)
    response = await client.get("/orders", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_order_by_id(client, auth_headers, product_variant):
    await client.post("/cart/items", json={"product_variant_id": product_variant["id"], "quantity": 2}, headers=auth_headers)
    await client.post("/orders", json={"delivery_address": "Kyiv, Khreshchatik 7"}, headers=auth_headers)
    order = await client.get("/orders", headers=auth_headers)
    order_id = order.json()[0]["id"]
    response = await client.get(f"/orders/{order_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == order_id