#define MICROPY_HW_BOARD_NAME       "STM-RF215"
#define MICROPY_HW_MCU_NAME         "STM32F411xE"

#define MICROPY_HW_ENABLE_INTERNAL_FLASH_STORAGE (0)
#define MICROPY_HW_HAS_SWITCH       (1)
#define MICROPY_HW_HAS_FLASH        (1)
#define MICROPY_HW_ENABLE_USB       (1)

// use external SPI flash for storage
#define MICROPY_HW_SPIFLASH_SIZE_BITS (32 * 1024 * 1024)
#define MICROPY_HW_SPIFLASH_CS      (pin_A4)
#define MICROPY_HW_SPIFLASH_SCK     (pin_A5)
#define MICROPY_HW_SPIFLASH_MISO    (pin_A6)
#define MICROPY_HW_SPIFLASH_MOSI    (pin_A7)

// block device config for SPI flash
extern const struct _mp_spiflash_config_t spiflash_config;
extern struct _spi_bdev_t spi_bdev;
#define MICROPY_HW_BDEV_IOCTL(op, arg) ( \
    (op) == BDEV_IOCTL_NUM_BLOCKS ? (MICROPY_HW_SPIFLASH_SIZE_BITS / 8 / FLASH_BLOCK_SIZE) : \
    (op) == BDEV_IOCTL_INIT ? spi_bdev_ioctl(&spi_bdev, (op), (uint32_t)&spiflash_config) : \
    spi_bdev_ioctl(&spi_bdev, (op), (arg)) \
)
#define MICROPY_HW_BDEV_READBLOCKS(dest, bl, n) spi_bdev_readblocks(&spi_bdev, (dest), (bl), (n))
#define MICROPY_HW_BDEV_WRITEBLOCKS(src, bl, n) spi_bdev_writeblocks(&spi_bdev, (src), (bl), (n))

// HSE is 26MHz, CPU freq set to 96MHz
#define MICROPY_HW_CLK_PLLM (26)
#define MICROPY_HW_CLK_PLLN (196)
#define MICROPY_HW_CLK_PLLP (RCC_PLLP_DIV2)
#define MICROPY_HW_CLK_PLLQ (4)

// UART config
#define MICROPY_HW_UART1_TX     (pin_A15)
#define MICROPY_HW_UART1_RX     (pin_B3)

// I2C busses
#define MICROPY_HW_I2C1_SCL     (pin_B8)
#define MICROPY_HW_I2C1_SDA     (pin_B9)

// SPI busses
#define MICROPY_HW_SPI2_NSS     (pin_A8)
#define MICROPY_HW_SPI2_SCK     (pin_B13)
#define MICROPY_HW_SPI2_MISO    (pin_B14)
#define MICROPY_HW_SPI2_MOSI    (pin_B15)

// USRSW has pulldown, pressing the buttons makes the input go high.
#define MICROPY_HW_USRSW_PIN 	    (pin_B7)
#define MICROPY_HW_USRSW_PULL       (GPIO_NOPULL)
#define MICROPY_HW_USRSW_EXTI_MODE  (GPIO_MODE_IT_RISING)
#define MICROPY_HW_USRSW_PRESSED    (1)

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
