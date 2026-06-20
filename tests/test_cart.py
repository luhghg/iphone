async def test_add_item_to_cart(client, product_variant, auth_headers):
    response = await client.post("/cart/items", json={"product_variant_id": product_variant["id"], "quantity": 2}, headers=auth_headers)
    assert response.status_code == 201


async def test_add_same_item_twice(client, product_variant, auth_headers):
    await client.post("/cart/items", json={"product_variant_id": product_variant["id"], "quantity": 2}, headers=auth_headers)
    response = await client.post("/cart/items", json={"product_variant_id": product_variant["id"], "quantity": 3}, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["quantity"] == 5


async def test_get_cart(client, product_variant, auth_headers):
    await client.post("/cart/items", json={"product_variant_id": product_variant["id"], "quantity": 2}, headers=auth_headers)
    response = await client.get("/cart", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1


async def test_delete_cart_item(client, auth_headers, product_variant):
    added = await client.post("/cart/items", json={"product_variant_id": product_variant["id"], "quantity": 2},
                                headers=auth_headers)
    item_id = added.json()["id"]
    response = await client.delete(f"/cart/items/{item_id}", headers=auth_headers)
    assert response.status_code == 204
    response = await client.get("/cart", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()["items"]) == 0


async def test_clear_cart(client, auth_headers, product_variant):
    await client.post("/cart/items", json={"product_variant_id": product_variant["id"], "quantity": 2},
                                headers=auth_headers)
    response = await client.delete("/cart/items", headers=auth_headers)
    assert response.status_code == 204
    response = await client.get("/cart", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()["items"]) == 0