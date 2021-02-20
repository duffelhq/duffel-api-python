from .fixtures import fixture


def test_create_order_cancellation(requests_mock):
    with fixture('create-order-cancellation', '/order_cancellations',
                 requests_mock.post) as client:
        cancellation = client.order_cancellations.create('order-id')
        assert cancellation.id == 'orc_001'
        assert cancellation.refund_to == 'arc_bsp_cash'
        assert cancellation.refund_currency == 'GBP'
        assert cancellation.refund_amount == '90.80'


def test_confirm_order_cancellation(requests_mock):
    with fixture('confirm-order-cancellation',
                 '/order_cancellations/some-id/actions/confirm',
                 requests_mock.post) as client:
        cancellation = client.order_cancellations.confirm('some-id')
        assert cancellation.id == 'orc_001'
        assert cancellation.refund_to == 'arc_bsp_cash'
        assert cancellation.refund_currency == 'GBP'
        assert cancellation.refund_amount == '90.80'
