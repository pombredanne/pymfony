# -*- coding: utf-8 -*-
# This file is part of the pymfony package.
#
# (c) Alexandre Quercia <alquerci@email.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from __future__ import absolute_import;

from os.path import dirname;

from pymfony.component.dependency import ContainerBuilder;
from pymfony.component.dependency.loader import JsonFileLoader
from pymfony.component.kernel.dependency import ConfigurableExtension;
from pymfony.component.config.definition import ConfigurationInterface;
from pymfony.component.config.definition.builder import TreeBuilder;
from pymfony.component.config import FileLocator;
from pymfony.component.config.definition.builder import ArrayNodeDefinition
from pymfony.component.console_kernel.routing import Router
from pymfony.component.console_kernel.routing import Route

"""
"""


class FrameworkExtension(ConfigurableExtension):
    def _loadInternal(self, config, container):
        assert isinstance(config, dict);
        assert isinstance(container, ContainerBuilder);

        loader = JsonFileLoader(container, FileLocator(
            dirname(__file__)+"/../Resources/config"
        ));

        loader.load("services.json");
        loader.load("console.json");


#        for name, value in config.items():
#            container.getParameterBag().set(self.getAlias()+'.'+name, value);

        container.setParameter('kernel.default_locale', config['default_locale']);

        if 'console' in config:
            self.__registerConsoleConfiguration(config['console'], container, loader);
        container.setParameter('console.router.resource', "");


    def getAlias(self):
        return 'framework';


    def __registerConsoleConfiguration(self, config, container, loader):
        assert isinstance(config, dict);

        container.setParameter('console.router.resource', config['resource']);



class Configuration(ConfigurationInterface):
    def getConfigTreeBuilder(self):
        treeBuilder = TreeBuilder();
        rootNode = treeBuilder.root('framework');

        node =  rootNode.children();
        node =      node.scalarNode('default_locale');
        node =          node.defaultValue("en");
        node =      node.end();
        node =  node.end();

        self.__addConsoleSection(rootNode);

        return treeBuilder;

    def __addConsoleSection(self, rootNode):
        assert isinstance(rootNode, ArrayNodeDefinition);

        rootNode\
            .children()\
                .arrayNode('console')\
                    .info('console configuration')\
                    .canBeUnset()\
                    .children()\
                        .scalarNode('resource').isRequired().end()\
                    .end()\
                .end()\
            .end()\
        ;
