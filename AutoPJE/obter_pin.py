def obter_pin():
    import keyring
    # Lê a senha da credencial: serviço=cert_digital_mario, usuário=cert_dig
    pin = keyring.get_password("cert_digital_mario", "cert_dig")
    if not pin:
        raise RuntimeError("PIN não encontrado no Gerenciador de Credenciais (cert_digital_mario / cert_dig).")
    return pin