import argparse
import os
import unittest

from quarkchain.cluster.cluster_config import ClusterConfig


class TestClusterConfig(unittest.TestCase):
    def test_cluster_dict_with_loadtest(self):
        """convert to dict and back to check if the content changed, requires `__eq__`
        removing --loadtest will make the test faster
        passing more num_shards will increase runtime linearly
        """
        parser = argparse.ArgumentParser()
        ClusterConfig.attach_arguments(parser)
        pwd = os.path.dirname(os.path.abspath(__file__))
        default_genesis_dir = os.path.join(pwd, "../../genesis_data")
        args = parser.parse_args(
            ["--num_shards=4", "--genesis_dir=" + default_genesis_dir]
        )
        cluster_config = ClusterConfig.create_from_args(args)

        args = parser.parse_args(["--cluster_config=" + cluster_config.json_filepath])
        deserialized = ClusterConfig.create_from_args(args)

        self.assertTrue(cluster_config == deserialized)
        full_shard_id = 0 | 4 | 0
        # 12000 loadtest accounts + ? alloc accounts
        self.assertGreaterEqual(
            len(cluster_config.QUARKCHAIN.shards[full_shard_id].GENESIS.ALLOC), 12000
        )

    def test_cluster_dict(self):
        parser = argparse.ArgumentParser()
        ClusterConfig.attach_arguments(parser)
        args = parser.parse_args(["--num_shards=4", "--genesis_dir="])
        cluster_config = ClusterConfig.create_from_args(args)

        args = parser.parse_args(["--cluster_config=" + cluster_config.json_filepath])
        deserialized = ClusterConfig.create_from_args(args)

        self.assertTrue(cluster_config == deserialized)
