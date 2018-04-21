#define MICROPY_HW_BOARD_NAME       "STM-RF215"
#define MICROPY_HW_MCU_NAME         "STM32F413xG"

#define MICROPY_HW_HAS_FLASH        (1)
#define MICROPY_HW_ENABLE_USB       (1)

// HSE is 26MHz, CPU freq set to 96MHz
#define MICROPY_HW_CLK_PLLM (26)
#define MICROPY_HW_CLK_PLLN (196)
#define MICROPY_HW_CLK_PLLP (RCC_PLLP_DIV2)
#define MICROPY_HW_CLK_PLLQ (4)

// UART config
#define MICROPY_HW_UART1_TX     (pin_A15)
#define MICROPY_HW_UART1_RX     (pin_B3)
// UART 2 connects to the STM32F103 (STLINK) on the Nucleo board
// and this is exposed as a USB Serial port.
#define MICROPY_HW_UART_REPL        PYB_UART_1
#define MICROPY_HW_UART_REPL_BAUD   115200

// I2C busses
#define MICROPY_HW_I2C1_SCL     (pin_B8)
#define MICROPY_HW_I2C1_SDA     (pin_B9)

// SPI busses
#define MICROPY_HW_SPI2_NSS     (pin_A8)
#define MICROPY_HW_SPI2_SCK     (pin_B13)
#define MICROPY_HW_SPI2_MISO    (pin_B14)
#define MICROPY_HW_SPI2_MOSI    (pin_B15)

// LEDs
#define MICROPY_HW_LED1             (pin_B0) // Red D1 LED
#define MICROPY_HW_LED2             (pin_B1) // Green D1 LED
#define MICROPY_HW_LED3             (pin_B10) // Blue D1 LED
#define MICROPY_HW_LED4             (pin_B6) // Green/PWR D3 LED
#define MICROPY_HW_LED_ON(pin)      (mp_hal_pin_low(pin))
#define MICROPY_HW_LED_OFF(pin)     (mp_hal_pin_high(pin))

// USB config
#define MICROPY_HW_USB_FS              (1)
//#define MICROPY_HW_USB_VBUS_DETECT_PIN (pin_A9)
