# Pub/Sub And Possible queue systems Data Visualization Application

## Overview

This application is designed to visualize data transportation using Pub/Sub. It helps users understand and monitor the flow of data between different components.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Demo](#demo)
- [Contributing](#contributing)
- [License](#license)

## Installation

To get started with the application, follow these steps:

1. Clone the repository:
   ```bash
   $ git clone https://github.com/Jonasdart/queues-monitor.git
   ```

2. Install dependencies using a package manager:
   ```bash
   $ pip install -r requirements.txt
   ```

3. Set up the configuration files:

    Generate your service account json, with PubSub Perms
    `.env`
    ```env
    GOOGLE_APPLICATION_CREDENTIALS="credentials.json"
    ```

    Configure your data labels. Way to organize and group your queued data.
    Important: This filters uses the content of queue message, configure according your reality
    `config.json`
    ```json
        {
        "fields": {
            "field_name": {
                "sub_group": "alternative_subgroup"
                },
            "field_name2": {
                "sub_group": "alternative_subgroup"
                }
            }
        }
    ```

    In the queues.spec file, configure your queues specifications. Example:

    `queues.spec`
   ```json
   {
    "queues": [{
        "id": "customer_x_data_processment",
        "alias": "Customer-X-Data",
        "provider": "GCP-PUBSUB|GCP-PUBSUB-LITE|AWS-SQS",
        "config": {
            "retentionType": "ONLY_ACK_MESSAGES",
            "frequency": "*/1 * * *",
            "range": 7
        },
        "pull": "projects/project_id/your/subscription_path",
        "reprocess": {
            "queue_endpoint": "projects/project_id/topics/your_queue_name",
            "attributes": {
                "foo": "bar"
            }
        }
    }]
}
   ```

## Usage

To use the application, in one terminal run the following command:

```bash
$ python start_consume.py
```

In another terminal, initialize the streamlit server:

```bash
$ streamlit run main.py
```

This will start the application and allow you to visualize Pub/Sub data transportation.

## Configuration

You can configure the application by modifying the `.env` file as explained in the Installation section.


## Contributing

We welcome contributions from the community. If you'd like to contribute, please follow these guidelines:

- Submit bug reports or feature requests through the [Issue Tracker](https://github.com/Jonasdart/queues-monitor/issues).
- Fork the repository, make changes, and submit a pull request with clear descriptions.
- Adhere to coding standards and best practices.

## License

This project is licensed under the [Your License Name] License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

We would like to thank the authors and organizations behind the libraries and tools used in this project for their contributions.

## Contact Information

If you have questions, feedback, or need support, you can reach out to us at [duarte.jsystem@gmail.com](mailto:duarte.jsystem@gmail.com).
