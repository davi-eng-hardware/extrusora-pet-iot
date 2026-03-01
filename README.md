# 🏭 Niobio Labs: SCADA & Telemetria para Extrusora PET (MVP de Bancada)

![C++](https://img.shields.io/badge/Firmware-C%2B%2B-blue?style=for-the-badge&logo=c%2B%2B)
![Python](https://img.shields.io/badge/SCADA-Python_3.14-yellow?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Mock_Prototype-success?style=for-the-badge)

## 📌 Visão Geral do Projeto
Projeto de P&D focado no desenvolvimento de uma arquitetura de controle e telemetria remota (IoT) para uma máquina de extrusão de garrafas PET. 

Este repositório contém a **Camada de Software (SCADA) e a Validação Lógica de Firmware**. Para garantir a segurança antes da integração com a eletrônica de potência real, este MVP foi construído como um teste de bancada (*Mocked Hardware*), simulando os atuadores físicos e sensores industriais.

---

## ⚙️ Arquitetura de Validação (Hardware de Bancada)

A lógica de controle em malha fechada (*closed-loop*) foi validada utilizando componentes de simulação em baixa tensão:

* **Simulação Térmica:** Um potenciômetro linear substitui temporariamente o termistor NTC, permitindo a injeção manual de dados analógicos para testar a resposta do sistema às variações de "temperatura".
* **Indicadores de Estado:** LEDs atuam como *flags* visuais para simular o chaveamento de potência (PWM) que futuramente irá para os transistores MOSFETs do bloco de aquecimento.
* **Atuação Mecânica:** Um motor DC de pequeno porte simula o motor de passo de tração, validando as rotinas de acoplamento e desacoplamento do filamento.
* **Interlock de Segurança:** O firmware bloqueia a rotação do motor caso a leitura do potenciômetro não atinja o *setpoint* mínimo, provando a eficácia do sistema contra a "extrusão a frio".

---

## 📡 Telemetria e Interface SCADA (Python)

O grande diferencial deste módulo é a interface HMI (Interface Homem-Máquina) rodando em ambiente Linux, desenvolvida para conversar via rádio frequência com a máquina.

* **Comunicação Direta:** Utilização de `socket.AF_BLUETOOTH` no Python, operando via protocolo RFCOMM (Bluetooth SPP) para transmissão de dados contínua e sem gargalos.
* **Full-Duplex Control:** O painel não apenas monitora o gráfico de temperatura em tempo real, mas envia comandos de *Override* (Sobrescrita) para forçar o acionamento mecânico direto pelo software.
* **Stack Visual:** Renderização reativa utilizando o framework **Flet**.

---

## 🎬 Demonstração do MVP (Lógica em Ação)

> **Clique na imagem abaixo para assistir ao teste de bancada no YouTube:**

[![Demonstração Niobio Labs](https://img.youtube.com/vi/oi7yjY_95QQ/maxresdefault.jpg)](https://youtu.be/oi7yjY_95QQ)

*(Acima: Teste da lógica de Interlock via simulação com potenciômetro e acionamento remoto do motor via painel SCADA).*

---

## 🚀 Próximos Passos (Integração Física)
A lógica testada neste MVP de bancada está pronta para ser acoplada à mecânica pesada.
1. **Merge de Hardware:** Substituição dos componentes simulados pela eletrônica de potência do projeto mecânico base.
2. **Calibração de Sensores:** Troca do potenciômetro pelo termistor 100k com a implementação da equação de *Steinhart-Hart* no firmware.
3. **Controle PID:** Refinamento do controle on/off dos LEDs para uma malha PID real chaveando o *hotend*.

---

## 🏛️ Contexto e Infraestrutura
Este módulo de IoT e Telemetria (*Niobio Labs*) foi desenvolvido de forma independente como uma camada de expansão tecnológica. Ele foi projetado para ser integrado à estrutura física e mecânica de uma Extrusora PET construída utilizando os recursos do **Laboratório Maker** da instituição publica, cujo é o Centro Federal de Educação Técnologica de Minas Gerais.
