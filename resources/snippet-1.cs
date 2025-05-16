private async Task<IResult> Handler(ISqlConnectionFactory connectionFactory)
{
    using var connection = connectionFactory.OpenConnection();

    var orders = await connection.QueryAsync<Order>(
        "SELECT * FROM \"Orders\"");

    return Results.Ok(orders);
}