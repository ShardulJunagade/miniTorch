import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import torch
import numpy as np
import pytest
import minitorch
from minitorch import Tensor, exp, log, relu, sigmoid, tanh
from minitorch.nn.modules.linear import Linear
from minitorch.nn.parameter import Parameter

def assert_tensor_allclose(t1, t2, atol=1e-6):
    assert np.allclose(np.array(t1.data), np.array(t2.detach().cpu().numpy()), atol=atol)
    if hasattr(t1, 'grad') and t1.grad is not None and t2.grad is not None:
        assert np.allclose(np.array(t1.grad), np.array(t2.grad.detach().cpu().numpy()), atol=atol)

def test_add():
    a = Tensor(2.0)
    b = Tensor(3.0)
    c = a + b
    t_a = torch.tensor(2.0, requires_grad=True)
    t_b = torch.tensor(3.0, requires_grad=True)
    t_c = t_a + t_b
    assert_tensor_allclose(c, t_c)
    c.backward()
    t_c.backward()
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)
    assert_tensor_allclose(b, t_b)
    assert np.allclose(b.grad, t_b.grad.detach().cpu().numpy(), atol=1e-6)

def test_mul():
    a = Tensor(2.0)
    b = Tensor(3.0)
    c = a * b
    t_a = torch.tensor(2.0, requires_grad=True)
    t_b = torch.tensor(3.0, requires_grad=True)
    t_c = t_a * t_b
    assert_tensor_allclose(c, t_c)
    c.backward()
    t_c.backward()
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)
    assert_tensor_allclose(b, t_b)
    assert np.allclose(b.grad, t_b.grad.detach().cpu().numpy(), atol=1e-6)

def test_pow():
    a = Tensor(2.0)
    c = a ** 3
    t_a = torch.tensor(2.0, requires_grad=True)
    t_c = t_a ** 3
    assert_tensor_allclose(c, t_c)
    c.backward()
    t_c.backward()
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)

def test_exp():
    a = Tensor(1.5)
    c = a.exp()
    t_a = torch.tensor(1.5, requires_grad=True)
    t_c = t_a.exp()
    assert_tensor_allclose(c, t_c)
    c.backward()
    t_c.backward()
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)

def test_log():
    a = Tensor(2.0)
    c = a.log()
    t_a = torch.tensor(2.0, requires_grad=True)
    t_c = t_a.log()
    assert_tensor_allclose(c, t_c)
    c.backward()
    t_c.backward()
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)

def test_neg():
    a = Tensor(2.0)
    c = -a
    t_a = torch.tensor(2.0, requires_grad=True)
    t_c = -t_a
    assert_tensor_allclose(c, t_c)
    c.backward()
    t_c.backward()
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)

def test_sub():
    a = Tensor(5.0)
    b = Tensor(3.0)
    c = a - b
    t_a = torch.tensor(5.0, requires_grad=True)
    t_b = torch.tensor(3.0, requires_grad=True)
    t_c = t_a - t_b
    assert_tensor_allclose(c, t_c)
    c.backward()
    t_c.backward()
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)
    assert_tensor_allclose(b, t_b)
    assert np.allclose(b.grad, t_b.grad.detach().cpu().numpy(), atol=1e-6)

def test_truediv():
    a = Tensor(6.0)
    b = Tensor(2.0)
    c = a / b
    t_a = torch.tensor(6.0, requires_grad=True)
    t_b = torch.tensor(2.0, requires_grad=True)
    t_c = t_a / t_b
    assert_tensor_allclose(c, t_c)
    c.backward()
    t_c.backward()
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)
    assert_tensor_allclose(b, t_b)
    assert np.allclose(b.grad, t_b.grad.detach().cpu().numpy(), atol=1e-6)

def test_matmul():
    a = Tensor([[1.0, 2.0], [3.0, 4.0]])
    b = Tensor([[2.0, 0.0], [1.0, 2.0]])
    c = a @ b
    t_a = torch.tensor([[1.0, 2.0], [3.0, 4.0]], requires_grad=True)
    t_b = torch.tensor([[2.0, 0.0], [1.0, 2.0]], requires_grad=True)
    t_c = t_a @ t_b
    assert_tensor_allclose(c, t_c)
    c.backward(np.ones_like(c.data))
    t_c.backward(torch.ones_like(t_c))
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)
    assert_tensor_allclose(b, t_b)
    assert np.allclose(b.grad, t_b.grad.detach().cpu().numpy(), atol=1e-6)

def test_radd():
    a = Tensor(2.0)
    c = 3.0 + a
    t_a = torch.tensor(2.0, requires_grad=True)
    t_c = 3.0 + t_a
    assert_tensor_allclose(c, t_c)
    c.backward()
    t_c.backward()
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)

def test_rsub():
    a = Tensor(2.0)
    c = 3.0 - a
    t_a = torch.tensor(2.0, requires_grad=True)
    t_c = 3.0 - t_a
    assert_tensor_allclose(c, t_c)
    c.backward()
    t_c.backward()
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)

def test_rmul():
    a = Tensor(2.0)
    c = 3.0 * a
    t_a = torch.tensor(2.0, requires_grad=True)
    t_c = 3.0 * t_a
    assert_tensor_allclose(c, t_c)
    c.backward()
    t_c.backward()
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)

def test_rtruediv():
    a = Tensor(2.0)
    c = 6.0 / a
    t_a = torch.tensor(2.0, requires_grad=True)
    t_c = 6.0 / t_a
    assert_tensor_allclose(c, t_c)
    c.backward()
    t_c.backward()
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)

def test_sum_function():
    # 1D sum
    a = minitorch.Tensor([1.0, 2.0, 3.0], requires_grad=True)
    c = minitorch.sum(a)
    t_a = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
    t_c = t_a.sum()
    assert np.allclose(c.data, t_c.detach().cpu().numpy())
    c.backward()
    t_c.backward()
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy())

    # 2D sum, axis=0
    a2 = minitorch.Tensor([[1.0, 2.0], [3.0, 4.0]], requires_grad=True)
    c2 = minitorch.sum(a2, axis=0)
    t_a2 = torch.tensor([[1.0, 2.0], [3.0, 4.0]], requires_grad=True)
    t_c2 = t_a2.sum(dim=0)
    assert np.allclose(c2.data, t_c2.detach().cpu().numpy())
    c2.backward(np.ones_like(c2.data))
    t_c2.backward(torch.ones_like(t_c2))
    assert np.allclose(a2.grad, t_a2.grad.detach().cpu().numpy())

    # 2D sum, axis=1, keepdims=True
    a3 = minitorch.Tensor([[1.0, 2.0], [3.0, 4.0]], requires_grad=True)
    c3 = minitorch.sum(a3, axis=1, keepdims=True)
    t_a3 = torch.tensor([[1.0, 2.0], [3.0, 4.0]], requires_grad=True)
    t_c3 = t_a3.sum(dim=1, keepdim=True)
    assert np.allclose(c3.data, t_c3.detach().cpu().numpy())
    c3.backward(np.ones_like(c3.data))
    t_c3.backward(torch.ones_like(t_c3))
    assert np.allclose(a3.grad, t_a3.grad.detach().cpu().numpy())

def test_exp_function():
    a = Tensor(1.5)
    c = exp(a)
    t_a = torch.tensor(1.5, requires_grad=True)
    t_c = t_a.exp()
    assert_tensor_allclose(c, t_c)
    c.backward()
    t_c.backward()
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)

def test_log_function():
    a = Tensor(2.0)
    c = log(a)
    t_a = torch.tensor(2.0, requires_grad=True)
    t_c = t_a.log()
    assert_tensor_allclose(c, t_c)
    c.backward()
    t_c.backward()
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)

def test_relu_function():
    a = Tensor([-1.0, 0.0, 2.0], requires_grad=True)
    c = relu(a)
    t_a = torch.tensor([-1.0, 0.0, 2.0], requires_grad=True)
    t_c = torch.relu(t_a)
    assert_tensor_allclose(c, t_c)
    c.backward(np.ones_like(c.data))
    t_c.backward(torch.ones_like(t_c))
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)

def test_sigmoid_function():
    a = Tensor([-1.0, 0.0, 2.0], requires_grad=True)
    c = sigmoid(a)
    t_a = torch.tensor([-1.0, 0.0, 2.0], requires_grad=True)
    t_c = torch.sigmoid(t_a)
    assert_tensor_allclose(c, t_c)
    c.backward(np.ones_like(c.data))
    t_c.backward(torch.ones_like(t_c))
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)

def test_tanh_function():
    a = Tensor([-1.0, 0.0, 2.0], requires_grad=True)
    c = tanh(a)
    t_a = torch.tensor([-1.0, 0.0, 2.0], requires_grad=True)
    t_c = torch.tanh(t_a)
    assert_tensor_allclose(c, t_c)
    c.backward(np.ones_like(c.data))
    t_c.backward(torch.ones_like(t_c))
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)

def test_leaky_relu_function():
    import torch.nn.functional as F
    a = Tensor([-1.0, 0.0, 2.0], requires_grad=True)
    c = minitorch.functional.leaky_relu(a, negative_slope=0.1)
    t_a = torch.tensor([-1.0, 0.0, 2.0], requires_grad=True)
    t_c = F.leaky_relu(t_a, negative_slope=0.1)
    assert_tensor_allclose(c, t_c)
    c.backward(np.ones_like(c.data))
    t_c.backward(torch.ones_like(t_c))
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)

def test_softmax_function():
    import torch.nn.functional as F
    a = Tensor([[1.0, 2.0, 3.0], [1.0, 2.0, 3.0]], requires_grad=True)
    c = minitorch.functional.softmax(a, dim=1)
    t_a = torch.tensor([[1.0, 2.0, 3.0], [1.0, 2.0, 3.0]], requires_grad=True)
    t_c = F.softmax(t_a, dim=1)
    assert_tensor_allclose(c, t_c)
    c.backward(np.ones_like(c.data))
    t_c.backward(torch.ones_like(t_c))
    assert_tensor_allclose(a, t_a)
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy(), atol=1e-6)

def test_linear_forward_and_backward():
    torch.manual_seed(42)
    np.random.seed(42)
    x_np = np.random.randn(4, 3)
    x = Tensor(x_np)
    x_torch = torch.tensor(x_np, dtype=torch.float32, requires_grad=True)
    minitorch_linear = Linear(3, 2)
    torch_linear = torch.nn.Linear(3, 2)
    torch_linear.weight.data = torch.tensor(minitorch_linear.weight.data, dtype=torch.float32)
    if minitorch_linear.bias is not None:
        torch_linear.bias.data = torch.tensor(minitorch_linear.bias.data, dtype=torch.float32)
    y = minitorch_linear(x)
    y_torch = torch_linear(x_torch)
    assert_tensor_allclose(y, y_torch)
    grad = np.ones_like(y.data)
    y.backward(grad)
    y_torch.backward(torch.ones_like(y_torch))
    assert np.allclose(np.array(minitorch_linear.weight.data), np.array(torch_linear.weight.data), atol=1e-6)
    if minitorch_linear.bias is not None:
        assert_tensor_allclose(minitorch_linear.bias, torch_linear.bias)
    assert_tensor_allclose(x, x_torch)

def test_parameter_zero_grad():
    p = Parameter(Tensor([1.0, 2.0, 3.0]))
    p.grad = Tensor([0.1, 0.2, 0.3])
    p.zero_grad()
    assert np.allclose(np.array(p.grad.data), 0.0)

def test_module_zero_grad():
    lin = Linear(3, 2)
    for param in lin.parameters():
        param.grad = Tensor(np.ones_like(param.data))
    lin.zero_grad()
    for param in lin.parameters():
        assert np.allclose(np.array(param.grad.data), 0.0)


# --- DTYPE TESTS FOR FLOAT32/BOOL ONLY ---
def test_tensor_dtype_construction_supported():
    a = Tensor([1, 2, 3], dtype=minitorch.float)
    assert a.data.dtype == minitorch.float32
    b = Tensor([True, False, True], dtype=minitorch.bool)
    assert b.data.dtype == minitorch.bool
    c = Tensor([1, 2, 3], dtype=minitorch.float32)
    assert c.data.dtype == minitorch.float32
    d = Tensor([True, False, True], dtype=minitorch.bool)
    assert d.data.dtype == minitorch.bool

def test_tensor_dtype_construction_unsupported():
    with pytest.raises(TypeError):
        Tensor([1, 2, 3], dtype='int32')
    with pytest.raises(TypeError):
        Tensor([1, 2, 3], dtype=int)
    with pytest.raises(TypeError):
        Tensor([1.0, 2.0, 3.0], dtype='float64')

def test_tensor_default_dtype():
    a = Tensor([1, 2, 3])
    assert a.data.dtype == minitorch.float32
    b = Tensor([True, False, True])
    assert b.data.dtype == minitorch.bool
    c = Tensor([1.0, 2.0, 3.0])
    assert c.data.dtype == minitorch.float32

def test_tensor_dtype_operations():
    a = Tensor([1, 2, 3], dtype=minitorch.float)
    b = Tensor([4, 5, 6], dtype=minitorch.float32)
    c = a + b
    assert c.data.dtype == minitorch.float32
    d = a * b
    assert d.data.dtype == minitorch.float32
    e = a ** 2
    assert e.data.dtype == minitorch.float32
    f = a - b
    assert f.data.dtype == minitorch.float32
    g = a / b
    assert g.data.dtype == minitorch.float32
    # Boolean operations
    h = Tensor([True, False, True], dtype=minitorch.bool)
    i = Tensor([False, True, True], dtype=minitorch.bool)
    j = h * i
    assert j.data.dtype == minitorch.bool

def test_tensor_grad_dtype():
    a = Tensor([1.0, 2.0, 3.0], dtype=minitorch.float, requires_grad=True)
    b = Tensor([4.0, 5.0, 6.0], dtype=minitorch.float32, requires_grad=True)
    c = a * b
    c.backward(np.ones_like(c.data, dtype=minitorch.float32))
    assert a.grad.dtype == minitorch.float32
    assert b.grad.dtype == minitorch.float32
    # Boolean tensor should not have grad
    d = Tensor([True, False, True], dtype=minitorch.bool)
    assert d.grad is None

# --- INDEXING AND SLICING TESTS ---
def test_tensor_indexing():
    a = minitorch.Tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], requires_grad=True)
    t_a = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], requires_grad=True)
    # Single index
    assert np.allclose(a[0].data, t_a[0].detach().cpu().numpy())
    # Slice
    assert np.allclose(a[:, 1].data, t_a[:, 1].detach().cpu().numpy())
    # 2D slice
    assert np.allclose(a[0:2, 1:3].data, t_a[0:2, 1:3].detach().cpu().numpy())

def test_tensor_indexing_backward():
    a = minitorch.Tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], requires_grad=True)
    t_a = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], requires_grad=True)
    out = a[1, 2] * 2.0
    t_out = t_a[1, 2] * 2.0
    out.backward()
    t_out.backward()
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy())

def test_tensor_slicing_backward():
    a = minitorch.Tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], requires_grad=True)
    t_a = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], requires_grad=True)
    out = a[:, 1:3].sum()
    t_out = t_a[:, 1:3].sum()
    out.backward()
    t_out.backward()
    assert np.allclose(a.grad, t_a.grad.detach().cpu().numpy())